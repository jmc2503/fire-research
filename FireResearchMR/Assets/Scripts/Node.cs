using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class Node
{
    public Vector3 worldPosition;
    public GameObject nodeObject;
    public int x;
    public int y;
    public int gCost;
    public int hCost;
    public Node parent;
    public bool walkable;
    public float fireHeight;


    private bool exit;
    private bool onFire;
    private bool hasPlayer;
    private bool hidden;
    private Material[] materials;
    private Transform fireTransform;

    public Node(int _x, int _y, Vector3 _worldPosition, GameObject _nodeObject, Material[] _materials, bool _walkable, float _fireHeight)
    {
        this.x = _x;
        this.y = _y;
        this.nodeObject = _nodeObject;
        this.worldPosition = _worldPosition;
        this.onFire = false;
        this.hasPlayer = false;
        this.hidden = false;
        this.exit = false;
        this.materials = _materials;
        this.fireTransform = nodeObject.transform.Find("MediumFlames");
        this.fireHeight = _fireHeight;

        this.walkable = _walkable;

        fireTransform.position = new Vector3(fireTransform.position.x, fireTransform.position.y + fireHeight, fireTransform.position.z);

        if (!walkable)
        {
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[4];
        }

    }

    public int fCost
    {
        get
        {
            return gCost + hCost;
        }
    }

    public bool Hidden
    {
        get { return hidden; }
        set
        {
            hidden = value;
            SetMaterial();
        }
    }

    public bool OnFire
    {
        get { return onFire; }
        set
        {
            onFire = value;
            SetMaterial();
        }
    }

    public bool HasPlayer
    {
        get { return hasPlayer; }
        set
        {
            hasPlayer = value;
            SetMaterial();
        }
    }

    public bool Exit
    {
        get { return exit; }
        set
        {
            exit = value;
            SetMaterial();
        }
    }

    private void SetMaterial()
    {

        if (this.hidden)
        {
            if (!this.exit)
            {
                nodeObject.GetComponent<Renderer>().enabled = false;
            }
            else
            {
                nodeObject.GetComponent<Renderer>().enabled = true;
            }
        }
        else
        {
            nodeObject.GetComponent<Renderer>().enabled = true;
        }

        if (this.onFire) //Fire takes priority in rendering
        {
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[1];
            fireTransform.gameObject.SetActive(true);
        }
        else
        {
            fireTransform.gameObject.SetActive(false);
            if (this.hasPlayer) //Has Player
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[2];
            }
            else if (!this.walkable) //Unwalkable
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[4];
            }
            else if (this.exit) //Exit
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[3];
            }
            else //Normal
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[0];
            }
        }

    }

    public static (int, int) operator -(Node self, Node other)
    {
        return (self.x - other.x, self.y - other.y);
    }


}
