using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MenuManagerAR : MonoBehaviour
{

    public GridManagerAR grid;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.A) || OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger))
        {
            grid.HideGridBoxes();
        }
    }
}
