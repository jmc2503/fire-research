using System;
using System.Collections.Generic;
using UnityEngine;

public class FireManager : MonoBehaviour
{
    [Header("SCRIPTS")]
    public GridManager gridManager;

    [Header("PARAMETERS")]
    public float FIRE_SPREAD_PROBABILITY;
    public bool AR_ENABLED;

    private List<Node> fireList = new List<Node>();

    public void StartFire(Node startNode)
    {
        startNode.OnFire = true;
        fireList.Add(startNode);
    }

    public void PutOutFire(Node currNode)
    {
        currNode.OnFire = false;
        fireList.Remove(currNode);
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

            if ((xDist == 0 && yDist <= viewDistance) || (yDist == 0 && xDist <= viewDistance))
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
