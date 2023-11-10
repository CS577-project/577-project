using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class HeadSynthesize : MonoBehaviour
{
    public RenderTexture DepthRT;
    public Material DepthMaterial;

    public RenderTexture SynthesizeRT;
    public Material SynthesizeMaterial;

    public MeshRenderer HeadMesh;
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
        HeadMesh.sharedMaterial = SynthesizeMaterial;
        cam.targetTexture = SynthesizeRT;
        cam.Render();

    }

}
