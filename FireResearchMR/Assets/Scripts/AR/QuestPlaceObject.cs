using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuestPlaceObject : MonoBehaviour
{

    public OVRInput.RawButton placeButton;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (OVRInput.GetDown(placeButton))
        {
            PlaceGrid();
        }
    }

    void PlaceGrid()
    {
        Debug.Log("Hello");
    }
}
