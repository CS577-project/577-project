using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class HeadSynthesize : MonoBehaviour
{
    public string ExportPath;
    public RenderTexture DepthRT;
    public Material DepthMaterial;

    public RenderTexture SynthesizeRT;
    public Material SynthesizeMaterial;

    public MeshRenderer HeadMesh;

    public Texture2D StylizedImage;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void Synthesize()
    {
        Camera cam = GetComponent<Camera>();
        if(cam != null )
        {
            Material mat_before = HeadMesh.sharedMaterial;
            // first snapshot the depth 
            SnapshotDepth(cam);
            // now let's do the synthesize
            DoSynthesize(cam);
            // save the result
            Save();
            HeadMesh.sharedMaterial = mat_before;

            AssetDatabase.Refresh();
        }
    }
    private void SnapshotDepth( Camera cam )
    {
        HeadMesh.sharedMaterial = DepthMaterial;
        cam.targetTexture = DepthRT;
        cam.Render();
    }

    private void DoSynthesize( Camera cam )
    {
        Material runtime_mat = GameObject.Instantiate(SynthesizeMaterial);
        runtime_mat.SetTexture("_StyleImage", StylizedImage);
        runtime_mat.SetTexture("_DepthImage", DepthRT);
        HeadMesh.sharedMaterial = runtime_mat;
        cam.targetTexture = SynthesizeRT;
        cam.Render();
        

    }
    private void Save()
    {
        // read back from render target
        RenderTexture.active = SynthesizeRT;
        Texture2D tex = new Texture2D(SynthesizeRT.width, SynthesizeRT.height);
        tex.ReadPixels(new Rect(0, 0, SynthesizeRT.width, SynthesizeRT.height), 0, 0);
        RenderTexture.active = null;

        byte[] bytes = tex.EncodeToJPG();
        File.WriteAllBytes(ExportPath + "/HeadBaseUV.jpg", bytes);
        GameObject.DestroyImmediate(tex);
    }

}
