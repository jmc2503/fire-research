using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FireManager : MonoBehaviour
{
    public Vector2 fireStartPoint;
    public float FIRE_SPREAD_PROBABILITY;
    public GridManager gridManager;

    private List<Node> firelist;


    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public void SpreadFire()
    {
        List<Node> newFires = new List<Node>();

        foreach (Node node in firelist)
        {
            if (Random.value <= FIRE_SPREAD_PROBABILITY)
            {

            }
        }
    }
}
