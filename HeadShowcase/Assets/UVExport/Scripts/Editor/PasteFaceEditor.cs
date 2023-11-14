using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(PasteFace))]
public class PasteFaceEditor : Editor
{
    public override void OnInspectorGUI()
    {
        PasteFace myTarget = (PasteFace)target;

        // Draw the default inspector.
        DrawDefaultInspector();

        // Add a button to the Inspector.
        if (GUILayout.Button("Do PasteFace"))
        {
            myTarget.DoPasteFace();
        }
    }
}
