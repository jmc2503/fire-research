using System.Collections;
using System.Collections.Generic;
using UnityEditor.iOS;
using UnityEngine;

public class Node
{
    public Vector3 worldPosition;
    public GameObject nodeObject;
    public int x;
    public int y;


    private bool onFire;
    private bool hasPlayer;
    private bool hidden;
    private Material[] materials;

    public Node(int _x, int _y, Vector3 _worldPosition, GameObject _nodeObject, Material[] _materials)
    {
        this.x = _x;
        this.y = _y;
        this.nodeObject = _nodeObject;
        this.worldPosition = _worldPosition;
        this.onFire = false;
        this.hasPlayer = false;
        this.hidden = true;
        this.materials = _materials;
    }

    public bool Hidden
    {
        get { return hidden; }
        set
        {
            hidden = value;
            SetFireMaterial(this.onFire);
        }
    }

    public bool OnFire
    {
        get { return onFire; }
        set
        {
            onFire = value;
            SetFireMaterial(value);
        }
    }

    public bool HasPlayer
    {
        get { return hasPlayer; }
        set
        {
            hasPlayer = value;
            SetPlayerMaterial(value);
        }
    }

    private void SetFireMaterial(bool value)
    {
        if (value && !this.hidden)
        {
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[1];
        }
        else
        {
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[0];
        }
    }

    private void SetPlayerMaterial(bool value)
    {
        if (value)
        {
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[2];
        }
        else
        {
            if (this.onFire)
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[1];
            }
            else
            {
                this.nodeObject.GetComponent<MeshRenderer>().material = materials[0];
            }
        }
    }
}
