using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class HeadSnapshot : MonoBehaviour
{
    public Material BaseColorMaterial;
    public RenderTexture BaseColorRT;
    public MeshRenderer HeadMesh;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void SnaptShot()
    {
        // do the snapshot via camera
        Camera cam = GetComponent<Camera>();
        if (cam != null) 
        {
            Material mat_before = HeadMesh.sharedMaterial;
            SnapshotBaseColor(cam);
            HeadMesh.sharedMaterial = mat_before;
            AssetDatabase.Refresh();
        }
    }
    private void SnapshotBaseColor( Camera cam )
    {
        HeadMesh.sharedMaterial = BaseColorMaterial;
        cam.targetTexture = BaseColorRT;
        cam.Render();
        string filepath = UtilFuncs.GetSaveDir("HeadBase.jpg");
        UtilFuncs.SaveTextureJPG(cam, BaseColorRT, filepath);
    }
   
}
