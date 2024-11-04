using System.Collections;
using System.Collections.Generic;
using UnityEditor.iOS;
using UnityEngine;

public class Node
{
    public static List<Material> materials;
    public Vector3 worldPosition;
    public GameObject nodeObject;

    private bool onFire;
    private bool hasPlayer;

    static Node()
    {
        materials = new List<Material> { Resources.Load<Material>("Materials/White"), Resources.Load<Material>("Materials/Fire"), Resources.Load<Material>("Materials/Player") };
    }

    public Node(Vector3 _worldPosition, GameObject _nodeObject)
    {
        this.nodeObject = _nodeObject;
        this.worldPosition = _worldPosition;
        this.onFire = false;
        this.hasPlayer = false;
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
        if (value)
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
            this.nodeObject.GetComponent<MeshRenderer>().material = materials[0];
        }
    }
}
