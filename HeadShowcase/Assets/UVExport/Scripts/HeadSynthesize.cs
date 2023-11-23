using JetBrains.Annotations;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class HeadSynthesize : MonoBehaviour
{
    public string ExportPath;
    /// <summary>
    /// render texture for depth
    /// </summary>
    public RenderTexture DepthRT;
    /// <summary>
    /// material for depth
    /// 
    /// </summary>
    public Material DepthMaterial;

    /// <summary>
    /// render texture for mask
    /// </summary>
    public RenderTexture MaskRT;
    /// <summary>
    /// 
    /// </summary>
    public Material MaskMaterial;

    public RenderTexture SynthesizeRT;
    public Material SynthesizeMaterial;

    public MeshRenderer HeadMesh;

    public Texture2D StylizedImage;
    public Texture2D MainTex;

    public Texture2D NewHeadTexture;
    public Texture2D OrigHeadTexture;

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
            string filepath = UtilFuncs.GetSaveDir("HeadBaseUV.png");
            UtilFuncs.SaveTexturePNG(cam, SynthesizeRT, filepath);
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
    private void SnapshotMask( Camera cam)
    {

    }

    private void DoSynthesize( Camera cam )
    {
        Graphics.Blit(MainTex, SynthesizeRT);
        Material runtime_mat = GameObject.Instantiate(SynthesizeMaterial);
        runtime_mat.SetTexture("_StyleImage", StylizedImage);
        runtime_mat.SetTexture("_DepthImage", DepthRT);
        HeadMesh.sharedMaterial = runtime_mat;
        // don't clear anything, I need the main tex color in Synthesize RenderTexture
        CameraClearFlags clear_flags = cam.clearFlags;
        cam.clearFlags = CameraClearFlags.Nothing;
        cam.targetTexture = SynthesizeRT;
        cam.Render();
        cam.clearFlags = clear_flags;
        

    }
    public void ReplaceHeadTexture()
    {
        if(NewHeadTexture == null)
        {
            return;
        }
        OrigHeadTexture = (Texture2D)HeadMesh.sharedMaterial.GetTexture("_MainTex");
        Material BaseInstMat = GameObject.Instantiate(HeadMesh.sharedMaterial);
        HeadMesh.sharedMaterial = BaseInstMat;
        HeadMesh.sharedMaterial.SetTexture("_MainTex", NewHeadTexture);
    }
    public void ResetHeadTexture()
    {
        HeadMesh.sharedMaterial.SetTexture("_MainTex", OrigHeadTexture);
    }


}
