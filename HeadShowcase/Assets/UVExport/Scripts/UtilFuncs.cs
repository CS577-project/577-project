using System.IO;
using UnityEngine;

public class UtilFuncs
{
    public static string GetSaveDir( string filename )
    {
        return Path.Combine("Assets/UVExport/Output", filename);
    }
    public static void SaveTexture(Camera cam, RenderTexture rt, string path)
    {
        RenderTexture.active = rt;
        Texture2D tex = new Texture2D(cam.targetTexture.width, cam.targetTexture.height);
        tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
        RenderTexture.active = null;
        byte[] bytes = tex.EncodeToJPG();
        File.WriteAllBytes(path, bytes);
        GameObject.DestroyImmediate(tex);
    }
}