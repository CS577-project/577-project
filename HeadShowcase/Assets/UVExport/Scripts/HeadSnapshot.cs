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
    public string ExportPath;
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
        // �����õ���ǰ���
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
        RenderTexture.active = BaseColorRT;
        Texture2D tex = new Texture2D(cam.targetTexture.width, cam.targetTexture.height);
        tex.ReadPixels(new Rect(0, 0, BaseColorRT.width, BaseColorRT.height), 0, 0);
        RenderTexture.active = null;
        byte[] bytes = tex.EncodeToJPG();
        File.WriteAllBytes(ExportPath + "/HeadBase.jpg", bytes);
        GameObject.DestroyImmediate(tex);

    }
   
}
