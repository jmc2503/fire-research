using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FloorSpawnAR : MonoBehaviour
{

    public static event Action<GameObject> OnFloorSpawned;
    public GameObject floorObject;

    void Start()
    {
        OnFloorSpawned?.Invoke(floorObject);
    }
}
