using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerManager : MonoBehaviour
{

    private Node currNode;
    private Node lastNode;
    public GridManager gridManager;
    public FireManager fireManager;

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

            //Spread the fire
            fireManager.SpreadFire();
        }

        lastNode = currNode;

    }
}
