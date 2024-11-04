using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerManager : MonoBehaviour
{

    private Node currNode;
    private Node lastNode;
    public GridManager gridManager;

    // Start is called before the first frame update
    void Start()
    {
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
        }

        lastNode = currNode;

    }
}
