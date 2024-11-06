using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FireManager : MonoBehaviour
{
    public float FIRE_SPREAD_PROBABILITY;
    public GridManager gridManager;

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
            if (Random.value <= FIRE_SPREAD_PROBABILITY)
            {
                //Spawn Fire
                List<Node> availableSpots = gridManager.GetAvailableFireSpread(node);

                if (availableSpots.Count > 0)
                {
                    Node fireNode = availableSpots[Random.Range(0, availableSpots.Count)];
                    newFires.Add(fireNode);
                    fireNode.OnFire = true;
                }
            }
        }

        fireList.AddRange(newFires);
    }
}
