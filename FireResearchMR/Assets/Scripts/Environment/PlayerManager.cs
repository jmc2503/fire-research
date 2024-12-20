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
    private List<GameObject> viewIndicators;
    private bool started = false;

    public void PlayerStart()
    {
        viewIndicators = new List<GameObject>();
        for (int i = -viewDistance; i <= viewDistance; i++)
        {
            for (int j = -viewDistance; j <= viewDistance; j++)
            {
                if (Math.Abs(i) + Math.Abs(j) <= viewDistance && Math.Abs(i) + Math.Abs(j) != 0)
                {
                    viewIndicators.Add(Instantiate(viewDistanceIndicator, Vector3.zero, Quaternion.identity));
                }
            }
        }

        started = true;

    }

    // Update is called once per frame
    void Update()
    {
        if (started)
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

    }

    void DrawViewIndicators(Node node)
    {

        List<Vector3> newPos = gridManager.GetIndicatorPositions(node, viewDistance);

        for (int i = 0; i < viewIndicators.Count; i++)
        {
            viewIndicators[i].transform.position = newPos[i];
        }
    }
}
