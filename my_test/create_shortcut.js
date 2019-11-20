
function CreateShortcut()
{
   wsh = new ActiveXObject('WScript.Shell');
   target_path = '"' + wsh.CurrentDirectory + '\\set_proxy.py"';
   icon_path = wsh.CurrentDirectory + '\\favicon-mac.ico';


   link = wsh.CreateShortcut(wsh.SpecialFolders("Desktop") + '\\GetProxy.lnk');
   link.TargetPath = target_path;
   link.Arguments = '';
   link.WindowStyle = 7;
   link.IconLocation = icon_path;
   link.Description = 'XX-Net';
   link.WorkingDirectory = wsh.CurrentDirectory;
   link.Save();
}


function main(){
    CreateShortcut();
}
main();
