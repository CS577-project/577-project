using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(HeadSynthesize))]
public class HeadSynthesizeEditor : Editor
{
    public override void OnInspectorGUI()
    {
        HeadSynthesize myTarget = (HeadSynthesize)target;

        // Draw the default inspector.
        DrawDefaultInspector();

        // Add a button to the Inspector.
        if (GUILayout.Button("Do Synthesize"))
        {
            myTarget.Synthesize();
        }
        if(GUILayout.Button("Replace Head Texture"))
        {
            myTarget.ReplaceHeadTexture();       
        }
        if(GUILayout.Button("Reset HeadTexture"))
        {
            myTarget.ResetHeadTexture();
        }
    }
}
