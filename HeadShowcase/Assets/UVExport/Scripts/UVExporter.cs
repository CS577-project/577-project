using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class UVExporter : MonoBehaviour
{
    public RenderTexture UVRT;
    public Material UVMaterial;
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
            Material mat_before = HeadMesh.material;
            SnapshotUV(cam);
            SnapshotBase(cam);
            HeadMesh.material = mat_before;
            AssetDatabase.Refresh();
        }
    }
    private void SnapshotUV( Camera cam )
    {
        HeadMesh.material = UVMaterial;
        cam.targetTexture = UVRT;
        cam.Render();
        RenderTexture.active = UVRT;
        Texture2D tex = new Texture2D(cam.targetTexture.width, cam.targetTexture.height);
        tex.ReadPixels(new Rect(0, 0, UVRT.width, UVRT.height), 0, 0);
        RenderTexture.active = null;
        byte[] bytes = tex.EncodeToPNG();
        File.WriteAllBytes(ExportPath + "/HeadUV.png", bytes);
        GameObject.DestroyImmediate(tex);

    }
    private void SnapshotBase( Camera cam )
    {
        HeadMesh.material = BaseColorMaterial;
        cam.targetTexture = BaseColorRT;
        cam.Render();
        RenderTexture.active = BaseColorRT;
        Texture2D tex = new Texture2D(cam.targetTexture.width, cam.targetTexture.height);
        tex.ReadPixels(new Rect(0, 0, BaseColorRT.width, BaseColorRT.height), 0, 0);
        RenderTexture.active = null;
        byte[] bytes = tex.EncodeToPNG();
        File.WriteAllBytes(ExportPath + "/HeadBase.png", bytes);
        GameObject.DestroyImmediate(tex);

    }
    /// <summary>
    /// ����һ�ž���style transfer������������ԭ��uv��ͼ��
    /// </summary>
    public void UnwrapUV()
    {

    }
}
