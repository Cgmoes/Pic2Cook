using Android.Hardware.Camera2;

namespace Pic2Cook
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        public MainPage()
        {
            InitializeComponent();
        }

        private void OnScanFridgeClicked(object sender, EventArgs e)
        {
            if (Permissions.CheckStatusAsync<Permissions.Camera>  PermissionStatus.Unknown) 
            {
            }
        }
    }

}
