using System;
using System.Collections.Generic;
using UnityEngine;

public class FireManagerAR : MonoBehaviour
{
    [Header("SCRIPTS")]
    public GridManagerAR gridManager;
    public PlayerPathFinderAR playerPathFinder;
    public PathFindingAR pathFinderAR;

    [Header("PARAMETERS")]
    public float FIRE_SPREAD_PROBABILITY;

    private List<Node> fireList = new List<Node>();

    public void StartFire(Node startNode)
    {
        startNode.OnFire = true;
        fireList.Add(startNode);
        playerPathFinder.fireNode = startNode;
        pathFinderAR.fireNode = startNode;
    }

    public void PutOutFire(Node currNode)
    {
        currNode.OnFire = false;
        fireList.Remove(currNode);

        if (pathFinderAR.fireNode == currNode && fireList.Count > 0)
        {
            pathFinderAR.fireNode = fireList[UnityEngine.Random.Range(0, fireList.Count)];
        }
    }

    public void SpreadFire()
    {
        List<Node> newFires = new List<Node>();

        foreach (Node node in fireList)
        {
            if (UnityEngine.Random.value <= FIRE_SPREAD_PROBABILITY)
            {
                //Spawn Fire
                List<Node> availableSpots = gridManager.GetAvailableFireSpread(node);

                if (availableSpots.Count > 0)
                {
                    Node fireNode = availableSpots[UnityEngine.Random.Range(0, availableSpots.Count)];
                    newFires.Add(fireNode);
                    fireNode.OnFire = true;
                }
            }
        }

        fireList.AddRange(newFires);
    }

    public void SetFireVisibility(Node currNode, int viewDistance)
    {
        foreach (Node fire in fireList)
        {
            int xDist = Math.Abs(fire.x - currNode.x);
            int yDist = Math.Abs(fire.y - currNode.y);

            if (xDist + yDist <= viewDistance)
            {
                fire.Hidden = false;
            }
            else
            {
                fire.Hidden = true;
            }
        }
    }
}
