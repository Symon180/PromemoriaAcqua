param(
    [Parameter(Mandatory = $true)]
    [string]$Title,

    [Parameter(Mandatory = $true)]
    [string]$Message
)

$ErrorActionPreference = "Stop"

function Escape-ToastXml {
    param([string]$Text)
    return [System.Security.SecurityElement]::Escape([string]$Text)
}

function Register-AcquaToastApp {
    $appId = "Symon.PromemoriaAcqua"
    $registryPath = "HKCU:\Software\Classes\AppUserModelId\$appId"
    New-Item -Path $registryPath -Force | Out-Null
    New-ItemProperty -Path $registryPath -Name "DisplayName" -Value "Promemoria Acqua" -PropertyType String -Force | Out-Null

    if (-not ("Acqua.Toast.NativeMethods" -as [type])) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
namespace Acqua.Toast {
    public static class NativeMethods {
        [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
        public static extern int SetCurrentProcessExplicitAppUserModelID(string appID);
    }
}
"@
    }
    [void][Acqua.Toast.NativeMethods]::SetCurrentProcessExplicitAppUserModelID($appId)
    return $appId
}

function Show-NativeToast {
    $appId = Register-AcquaToastApp

    $titleXml = Escape-ToastXml $Title
    $messageXml = Escape-ToastXml $Message

    $toastXml = @"
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>$titleXml</text>
      <text>$messageXml</text>
    </binding>
  </visual>
  <actions>
    <action content="Ho bevuto" arguments="dismiss" activationType="system" />
  </actions>
  <audio src="ms-winsoundevent:Notification.Default" />
</toast>
"@

    [void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
    [void][Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime]
    [void][Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]

    $xmlDocument = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xmlDocument.LoadXml($toastXml)
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xmlDocument
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId)
    $notifier.Show($toast)
    Start-Sleep -Milliseconds 500
}

try {
    Show-NativeToast
}
catch {}
