using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(HeadUnwrapUV))]
public class HeadUnwrapUVEditor : Editor
{
    public override void OnInspectorGUI()
    {
        HeadUnwrapUV myTarget = (HeadUnwrapUV)target;

        // Draw the default inspector.
        DrawDefaultInspector();

        // Add a button to the Inspector.
        if (GUILayout.Button("Do UnwrapUV"))
        {
            myTarget.DoUnwrapUV();
        }
    }
}
