using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;

public class PlayerManager : MonoBehaviour
{
    [Header("SCRIPTS")]
    public GridManager gridManager;
    public FireManager fireManager;

    [Header("PARAMETERS")]
    public int viewDistance;

    [Header("GAMEOBJECTS")]
    public GameObject viewDistanceIndicator;

    private Node currNode;
    private Node lastNode;
    private GameObject[,] viewIndicators;

    void Start()
    {
        viewIndicators = new GameObject[4, viewDistance];
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < viewDistance; j++)
            {
                viewIndicators[i, j] = Instantiate(viewDistanceIndicator, Vector3.zero, Quaternion.identity);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        currNode = gridManager.GetNodeFromWorldPoint(transform.position);

        if (currNode != lastNode)
        {
            currNode.HasPlayer = true;
            if (lastNode != null)
            {
                lastNode.HasPlayer = false;
            }

            //Put out the fire
            if (currNode.OnFire)
            {
                fireManager.PutOutFire(currNode);
            }

            //Spread the fire and checkvisibilty
            fireManager.SpreadFire();
            fireManager.SetFireVisibility(currNode, viewDistance);
            DrawViewIndicators(currNode);
        }

        lastNode = currNode;

    }

    void DrawViewIndicators(Node node)
    {

        Vector3[,] newPos = gridManager.GetIndicatorPositions(currNode, viewDistance);

        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < viewDistance; j++)
            {
                viewIndicators[i, j].transform.position = newPos[i, j];
            }
        }
    }
}
