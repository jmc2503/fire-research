using System;
using System.Collections;
using System.Collections.Generic;
using Unity.Mathematics;
using UnityEngine;

public class GridManagerAR : MonoBehaviour
{
    [Header("SCRIPTS")]
    public FireManagerAR fireManager;
    public PlayerManagerAR playerManager;

    [Header("PARAMETERS")]
    public int GridRows;
    public int GridColumns;
    public float BoxSeparation;
    public Vector3 gridStartingCorner;

    [Header("GAMEOBJECTS")]
    private GameObject gridFloor;
    public GameObject gridBox;
    public Material[] materials;

    private float nodeRadius;
    private Node[,] grid;
    private float widthJump;
    private float heightJump;
    private Vector2 gridWorldSize;
    private bool gridBoxesHidden = false;

    private void OnEnable()
    {
        FloorSpawnAR.OnFloorSpawned += ARStart;
    }

    private void OnDisable()
    {
        FloorSpawnAR.OnFloorSpawned -= ARStart;
    }

    // Start is called before the first frame update
    public void ARStart(GameObject floor)
    {
        gridFloor = floor;
        Renderer renderer = gridBox.GetComponent<Renderer>();
        Vector3 gridBoxSize = renderer.bounds.size;

        //Establish constants
        widthJump = gridBoxSize.x + BoxSeparation;
        heightJump = gridBoxSize.z + BoxSeparation;

        SetPlaneVariables(gridFloor);

        gridWorldSize.x = widthJump * GridRows;
        gridWorldSize.y = heightJump * GridColumns;

        nodeRadius = widthJump / 2;

        grid = new Node[GridRows, GridColumns];

        CreateGrid(grid);
        if (playerManager != null)
        {
            playerManager.PlayerStart();
            fireManager.StartFire(GetRandomStartNode());
        }
    }

    Node GetRandomStartNode()
    {
        int x = UnityEngine.Random.Range(0, GridRows);
        int y = UnityEngine.Random.Range(0, GridColumns);

        return grid[x, y];
    }


    public void CreateGrid(Node[,] grid)
    {

        for (int i = 0; i < GridRows; i++)
        {
            for (int j = 0; j < GridColumns; j++)
            {
                Vector3 worldPos = new Vector3(gridStartingCorner.x + (i * widthJump + nodeRadius), gridStartingCorner.y, gridStartingCorner.z + (j * heightJump + nodeRadius));
                grid[i, j] = new Node(i, j, worldPos, Instantiate(gridBox, worldPos, Quaternion.identity), materials, true);
            }
        }
    }

    public Node GetNodeFromWorldPoint(Vector3 worldPos)
    {
        //float percentX = (worldPos.x + gridWorldSize.x / 2) / gridWorldSize.x;
        //float percentY = (worldPos.z + gridWorldSize.y / 2) / gridWorldSize.y;
        float percentX = (worldPos.x - gridStartingCorner.x) / gridWorldSize.x;
        float percentY = (worldPos.z - gridStartingCorner.z) / gridWorldSize.y;
        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.FloorToInt(Mathf.Clamp(GridRows * percentX, 0, GridRows - 1));
        int y = Mathf.FloorToInt(Mathf.Clamp(GridColumns * percentY, 0, GridColumns - 1));

        return grid[x, y];
    }

    public List<Node> GetAvailableFireSpread(Node node)
    {
        int x = node.x;
        int y = node.y;
        List<Node> availableNodes = new List<Node>();

        if (x - 1 >= 0)
        {
            if (!grid[x - 1, y].OnFire && !grid[x - 1, y].HasPlayer)
            {
                availableNodes.Add(grid[x - 1, y]);
            }
        }
        if (x + 1 < GridRows)
        {
            if (!grid[x + 1, y].OnFire && !grid[x + 1, y].HasPlayer)
            {
                availableNodes.Add(grid[x + 1, y]);
            }
        }
        if (y - 1 >= 0)
        {
            if (!grid[x, y - 1].OnFire && !grid[x, y - 1].HasPlayer)
            {
                availableNodes.Add(grid[x, y - 1]);
            }
        }
        if (y + 1 < GridColumns)
        {
            if (!grid[x, y + 1].OnFire && !grid[x, y + 1].HasPlayer)
            {
                availableNodes.Add(grid[x, y + 1]);
            }
        }
        return availableNodes;
    }

    public Node GetNodeFromCoords(Node node, int new_x, int new_y)
    {
        int checkX = node.x + new_x;
        int checkY = node.y + new_y;

        if (checkX >= 0 && checkX < GridRows && checkY >= 0 && checkY < GridColumns)
        {
            return grid[checkX, checkY];
        }

        return node;
    }

    public void HideGridBoxes()
    {
        if (gridBoxesHidden)
        {
            foreach (Node node in grid)
            {
                node.nodeObject.GetComponent<Renderer>().enabled = false;
            }
        }
        else
        {
            foreach (Node node in grid)
            {
                node.nodeObject.GetComponent<Renderer>().enabled = true;
            }
        }

        gridBoxesHidden = !gridBoxesHidden;
    }

    public List<Node> GetNeighbors(Node node)
    {
        List<Node> neighbors = new List<Node>();

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0)
                {
                    continue;
                }

                int checkX = node.x + x;
                int checkY = node.y + y;

                if (checkX >= 0 && checkX < GridRows && checkY >= 0 && checkY < GridColumns)
                {
                    neighbors.Add(grid[checkX, checkY]);
                }
            }
        }

        return neighbors;
    }

    public List<Vector3> GetIndicatorPositions(Node currNode, int viewDistance)
    {
        List<Vector3> positions = new List<Vector3>();

        for (int i = -viewDistance; i <= viewDistance; i++)
        {
            for (int j = -viewDistance; j <= viewDistance; j++)
            {
                if (Math.Abs(i) + Math.Abs(j) <= viewDistance && Math.Abs(i) + Math.Abs(j) != 0)
                {
                    Vector3 newPos = currNode.worldPosition;
                    newPos.x += j * widthJump;
                    newPos.z += i * widthJump;
                    positions.Add(newPos);
                }
            }
        }

        return positions;
    }

    void SetPlaneVariables(GameObject plane)
    {
        if (plane != null)
        {
            Bounds bounds = plane.GetComponent<MeshFilter>().mesh.bounds;
            //Vector3 bottomLeftCorner = plane.transform.TransformPoint(new Vector3(bounds.min.x, bounds.min.y, bounds.min.z));
            //Vector3 topRightCorner = plane.transform.TransformPoint(new Vector3(bounds.max.x, bounds.max.y, bounds.max.z));

            Debug.Log("Local Bounds Min: " + bounds.min);
            Debug.Log("Local Bounds Max: " + bounds.max);

            Vector3 bottomLeftCorner = plane.transform.TransformPoint(bounds.min);
            Vector3 topRightCorner = plane.transform.TransformPoint(bounds.max);

            gridStartingCorner.x = Math.Min(bottomLeftCorner.x, topRightCorner.x);
            gridStartingCorner.y = bottomLeftCorner.y + 0.1f;
            gridStartingCorner.z = Math.Min(bottomLeftCorner.z, topRightCorner.z);

            GridRows = (int)Math.Floor(Math.Abs(topRightCorner.x - bottomLeftCorner.x) / widthJump);
            GridColumns = (int)Math.Floor(Math.Abs(topRightCorner.z - bottomLeftCorner.z) / heightJump);

            Debug.Log(bottomLeftCorner);
            Debug.Log(topRightCorner);
            Debug.Log((GridRows, GridColumns));

        }
    }
}
