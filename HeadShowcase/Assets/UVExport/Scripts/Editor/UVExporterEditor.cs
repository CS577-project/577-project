using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(UVExporter))]
public class UVExporterEditor : Editor
{
    public override void OnInspectorGUI()
    {
        UVExporter myTarget = (UVExporter)target;

        // Draw the default inspector.
        DrawDefaultInspector();

        // Add a button to the Inspector.
        if (GUILayout.Button("Custom Function"))
        {
            myTarget.SnaptShot();
        }
    }
}
