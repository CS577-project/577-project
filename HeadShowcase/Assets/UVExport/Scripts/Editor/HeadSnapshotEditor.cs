using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(HeadSnapshot))]
public class HeadSnapshotEditor : Editor
{
    public override void OnInspectorGUI()
    {
        HeadSnapshot myTarget = (HeadSnapshot)target;

        // Draw the default inspector.
        DrawDefaultInspector();

        // Add a button to the Inspector.
        if (GUILayout.Button("Do Snapshot"))
        {
            myTarget.SnaptShot();
        }
    }
}
