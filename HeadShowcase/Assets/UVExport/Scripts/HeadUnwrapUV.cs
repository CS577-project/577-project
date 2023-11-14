using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class HeadUnwrapUV : MonoBehaviour
{
    public Material UnwrapUVMaterial;
    public RenderTexture UnwrapUVRT;
    public MeshRenderer HeadMesh;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void DoUnwrapUV()
    { 
           // do the snapshot via camera
        Camera cam = GetComponent<Camera>();
        if (cam != null)
        {
            Material mat_before = HeadMesh.sharedMaterial;
            Material UnwrapUVMaterial_Inst = GameObject.Instantiate(UnwrapUVMaterial);
            HeadMesh.sharedMaterial = UnwrapUVMaterial_Inst;
            cam.targetTexture = UnwrapUVRT;
            cam.Render();
            HeadMesh.sharedMaterial = mat_before;

            string filepath = UtilFuncs.GetSaveDir("UnwrappedFaceTexture.jpg");
            UtilFuncs.SaveTexture(cam, UnwrapUVRT, filepath);
            AssetDatabase.Refresh();
        }
    }

}
