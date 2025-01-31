using System.Collections;
using System.Collections.Generic;
using Meta.XR.MRUtilityKit;
using UnityEngine;

public class MenuManagerAR : MonoBehaviour
{

    public GridManagerAR grid;
    public Material effectMeshMaterial;
    public EffectMesh effectmesh;

    private bool flag = false;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.A) || OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger))
        {
            grid.HideGridBoxes();
        }

        if (Input.GetKeyDown(KeyCode.B) || OVRInput.GetDown(OVRInput.Button.SecondaryIndexTrigger))
        {
            if (flag)
            {
                effectmesh.HideMesh = true;
                flag = !flag;
            }
            else
            {
                effectmesh.HideMesh = false;
                flag = !flag;
            }
        }
    }
}
