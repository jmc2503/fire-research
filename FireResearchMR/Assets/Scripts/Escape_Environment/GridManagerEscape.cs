using System;
using System.Collections;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;
using UnityEngine;
using UnityEngine.Video;

public class GridManagerEscape : MonoBehaviour
{
    [Header("PARAMETERS")]
    public float BoxSeparation;
    public float FireSpreadProbability;

    [Header("GAMEOBJECTS")]
    public GameObject user; // The user object
    public GameObject gridPlane; // The plane that the grid is placed on
    public GameObject gridBox; // The box prefab placed for each grid space
    public Material[] materials; // The materials that the grid boxes can be

    public PlayerControllerEscape playerControllerEscape;

    private EscapePathFinder pathFinder;

    private Node[,] grid; // The grid of nodes
    private Node[] exitList = new Node[4]; // List of exits on each side of the grid
    private List<Node> fireList;
    private float nodeRadius; // The radius of each node

    private float widthJump; //horizontal distance between each grid space
    private float heightJump; //vertical distance between each grid space
    private int GridRows; //# of rows in the grid
    private int GridColumns; //# of cols in the grid
    private Vector3 gridStartingCorner;
    private Vector2 gridWorldSize; //total grid Size

    private Node lastNode;

    // Start is called before the first frame update
    void Start()
    {
        pathFinder = GetComponent<EscapePathFinder>();

        Vector3 gridBoxSize = gridBox.GetComponent<Renderer>().bounds.size;

        widthJump = gridBoxSize.x + BoxSeparation;
        heightJump = gridBoxSize.z + BoxSeparation;

        SetPlaneVariables(gridPlane);

        gridWorldSize.x = widthJump * GridRows;
        gridWorldSize.y = heightJump * GridColumns;

        nodeRadius = widthJump / 2;

        grid = new Node[GridRows, GridColumns];
        fireList = new List<Node>();

        CreateGrid();
        CreateExits();
        CreateFire();
    }

    void Update()
    {
        if (user != null)
        {
            Node currNode = GetNodeFromWorldPoint(user.transform.position);
            if (currNode != lastNode)
            {
                currNode.HasPlayer = true;
                if (lastNode != null)
                {
                    lastNode.HasPlayer = false;
                }

                if (currNode.OnFire == true)
                {
                    playerControllerEscape.DamagePlayer(10);
                }

                SpreadFire();

                int shortestPathLength = int.MaxValue;
                List<Node> shortestPath = null;

                //Find all paths
                foreach (Node exit in exitList)
                {
                    List<Node> newPath = pathFinder.FindPath(currNode.worldPosition, exit.worldPosition);

                    if (newPath != null && newPath.Count < shortestPathLength)
                    {
                        shortestPathLength = newPath.Count;
                        shortestPath = newPath;
                    }
                }

                pathFinder.DrawPath(shortestPath);
            }

            lastNode = currNode;
        }
    }

    void CreateExits()
    {
        exitList[0] = grid[0, UnityEngine.Random.Range(0, GridColumns)];
        exitList[1] = grid[GridRows - 1, UnityEngine.Random.Range(0, GridColumns)];
        exitList[2] = grid[UnityEngine.Random.Range(0, GridRows), 0];
        exitList[3] = grid[UnityEngine.Random.Range(0, GridRows), GridColumns - 1];

        foreach (Node exit in exitList)
        {
            exit.Exit = true;
        }
    }

    void CreateGrid()
    {
        for (int i = 0; i < GridRows; i++)
        {
            for (int j = 0; j < GridColumns; j++)
            {
                Vector3 worldPos = new Vector3(gridStartingCorner.x + (i * widthJump + nodeRadius), gridStartingCorner.y, gridStartingCorner.z + (j * heightJump + nodeRadius));
                grid[i, j] = new Node(i, j, worldPos, Instantiate(gridBox, worldPos, Quaternion.identity), materials);
            }
        }
    }

    void CreateFire()
    {
        int x = UnityEngine.Random.Range(0, GridRows);
        int y = UnityEngine.Random.Range(0, GridColumns);

        grid[x, y].OnFire = true;
        fireList.Add(grid[x, y]);
    }

    void SpreadFire()
    {
        List<Node> newFires = new List<Node>();

        foreach (Node node in fireList)
        {
            if (UnityEngine.Random.value <= FireSpreadProbability)
            {

                List<Node> availableSpots = GetNeighbors(node);

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

    public List<Node> GetNeighbors(Node node)
    {
        int x = node.x;
        int y = node.y;

        List<Node> neighbors = new List<Node>();

        if (x - 1 >= 0)
        {
            neighbors.Add(grid[x - 1, y]);
        }
        if (x + 1 < GridRows)
        {
            neighbors.Add(grid[x + 1, y]);
        }
        if (y - 1 >= 0)
        {
            neighbors.Add(grid[x, y - 1]);
        }
        if (y + 1 < GridColumns)
        {
            neighbors.Add(grid[x, y + 1]);
        }


        return neighbors;
    }

    public Node GetNodeFromWorldPoint(Vector3 worldPos)
    {
        float percentX = (worldPos.x - gridStartingCorner.x) / gridWorldSize.x;
        float percentY = (worldPos.z - gridStartingCorner.z) / gridWorldSize.y;
        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.FloorToInt(Mathf.Clamp(GridRows * percentX, 0, GridRows - 1));
        int y = Mathf.FloorToInt(Mathf.Clamp(GridColumns * percentY, 0, GridColumns - 1));

        return grid[x, y];
    }

    void SetPlaneVariables(GameObject plane)
    {
        if (plane != null)
        {
            Bounds bounds = plane.GetComponent<MeshFilter>().mesh.bounds;
            Vector3 bottomLeftCorner = plane.transform.TransformPoint(new Vector3(bounds.min.x, bounds.min.y, bounds.min.z));
            Vector3 topRightCorner = plane.transform.TransformPoint(new Vector3(bounds.max.x, bounds.max.y, bounds.max.z));

            gridStartingCorner.x = bottomLeftCorner.x;
            gridStartingCorner.y = bottomLeftCorner.y + 0.1f;
            gridStartingCorner.z = bottomLeftCorner.z;

            GridRows = (int)Math.Floor((topRightCorner.x - bottomLeftCorner.x) / widthJump);
            GridColumns = (int)Math.Floor((topRightCorner.z - bottomLeftCorner.z) / heightJump);
        }
    }
}
