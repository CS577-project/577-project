using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class PasteFace : MonoBehaviour
{
    public MeshRenderer HeadMesh;
    public Material PasteFaceMat;
    public RenderTexture PasteFaceRT;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void DoPasteFace()
    {
        // do the snapshot via camera
        Camera cam = GetComponent<Camera>();
        if (cam != null)
        {
            Material mat_before = HeadMesh.sharedMaterial;
            Material PasteFaceMat_Inst = GameObject.Instantiate(PasteFaceMat);
            HeadMesh.sharedMaterial = PasteFaceMat_Inst ;
            cam.targetTexture = PasteFaceRT;
            cam.Render();
            HeadMesh.sharedMaterial = mat_before;

            string filepath = UtilFuncs.GetSaveDir("PasteFaceResult.jpg");
            UtilFuncs.SaveTexture(cam, PasteFaceRT, filepath);
            AssetDatabase.Refresh();
        }

    }
}
