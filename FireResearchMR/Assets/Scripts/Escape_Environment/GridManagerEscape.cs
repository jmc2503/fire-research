using System;
using System.Collections;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;
using Meta.XR.MRUtilityKit;
using TMPro;
using UnityEngine;
using UnityEngine.Video;
using UnityEngine.UI;

public class GridManagerEscape : MonoBehaviour
{
    [Header("PARAMETERS")]
    public bool AREnabled;
    public float BoxSeparation;
    public float FireSpreadProbability;
    public LayerMask unwalkableMask;

    [Header("GAMEOBJECTS")]
    public GameObject user; // The user object
    public GameObject gridPlane; // The plane that the grid is placed on
    public GameObject gridBox; // The box prefab placed for each grid space
    public Material[] materials; // The materials that the grid boxes can be

    [Header("UI")]
    public Slider fireSpreadProbSlider;
    public TextMeshProUGUI fireSpreadProbText;
    public Toggle gridBoxesToggle;
    public Toggle effectMeshToggle;
    public EffectMesh effectMesh;

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
    private bool start = false; //Check if the start has been completed
    private bool gridBoxesHidden = false; //Check if the grid boxes are hidden

    private Node lastNode;

    private Vector3 horizontalDirection;
    private Vector3 verticalDirection;

    private void OnEnable()
    {
        FloorSpawnAR.OnFloorSpawned += ARStart;
    }

    private void OnDisable()
    {
        FloorSpawnAR.OnFloorSpawned -= ARStart;
    }

    // Start is called before the first frame update
    void Start()
    {
        pathFinder = GetComponent<EscapePathFinder>();


        gridBoxesToggle.onValueChanged.AddListener(ToggleGridBoxesHidden);
        effectMeshToggle.onValueChanged.AddListener(ToggleEffectMesh);

        fireSpreadProbSlider.value = FireSpreadProbability;
        fireSpreadProbText.text = "Fire Spread Probability: " + FireSpreadProbability;
        fireSpreadProbSlider.onValueChanged.AddListener(UpdateFireSpreadProb);

        if (!AREnabled)
        {
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

            start = true;
        }
    }

    public void ARStart(GameObject floor)
    {
        gridPlane = floor;
        Vector3 gridBoxSize = gridBox.GetComponent<Renderer>().bounds.size;

        widthJump = gridBoxSize.x + BoxSeparation;
        heightJump = gridBoxSize.z + BoxSeparation;

        SetPlaneVariables(gridPlane);

        gridWorldSize.x = widthJump * GridRows;
        gridWorldSize.y = heightJump * GridColumns;

        Debug.Log(gridWorldSize);


        nodeRadius = widthJump / 2;

        grid = new Node[GridRows, GridColumns];
        fireList = new List<Node>();

        CreateGrid();
        CreateExits();
        CreateFire();

        start = true;
    }

    public void Reset()
    {
        foreach (Node node in grid)
        {
            node.OnFire = false;
            node.HasPlayer = false;
        }

        foreach (Node exit in exitList)
        {
            exit.Exit = false;
        }

        fireList.Clear();
        CreateExits();
        CreateFire();
    }

    void Update()
    {
        if (user != null && start)
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
        Vector3 normal = Vector3.Cross(horizontalDirection, verticalDirection).normalized;

        for (int i = 0; i < GridRows; i++)
        {
            for (int j = 0; j < GridColumns; j++)
            {
                Vector3 worldPos = gridStartingCorner + (horizontalDirection * i * widthJump) + (verticalDirection * j * heightJump);
                worldPos += (nodeRadius * horizontalDirection);
                worldPos += (nodeRadius * verticalDirection);

                Quaternion rotation = Quaternion.LookRotation(verticalDirection, normal);

                //Vector3 worldPos = new Vector3(gridStartingCorner.x + (i * widthJump + nodeRadius), gridStartingCorner.y, gridStartingCorner.z + (j * heightJump + nodeRadius));
                bool walkable = !Physics.CheckSphere(worldPos, nodeRadius * 0.9f, unwalkableMask);
                grid[i, j] = new Node(i, j, worldPos, Instantiate(gridBox, worldPos, rotation), materials, walkable);
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

    void UpdateFireSpreadProb(float value)
    {
        FireSpreadProbability = value;
        fireSpreadProbText.text = "Fire Spread Probability: " + FireSpreadProbability;
    }

    void ToggleGridBoxesHidden(bool value)
    {
        HideGridBoxes();
    }

    void ToggleEffectMesh(bool value)
    {
        if (value)
        {
            effectMesh.HideMesh = false;
        }
        else
        {
            effectMesh.HideMesh = true;
        }
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
            if (grid[x - 1, y].walkable && grid[x - 1, y].OnFire == false)
            {
                neighbors.Add(grid[x - 1, y]);
            }
        }
        if (x + 1 < GridRows)
        {
            if (grid[x + 1, y].walkable && grid[x + 1, y].OnFire == false)
            {
                neighbors.Add(grid[x + 1, y]);
            }
        }
        if (y - 1 >= 0)
        {
            if (grid[x, y - 1].walkable && grid[x, y - 1].OnFire == false)
            {
                neighbors.Add(grid[x, y - 1]);
            }
        }
        if (y + 1 < GridColumns)
        {
            if (grid[x, y + 1].walkable && grid[x, y + 1].OnFire == false)
            {
                neighbors.Add(grid[x, y + 1]);
            }
        }


        return neighbors;
    }

    public Node GetNodeFromWorldPoint(Vector3 worldPos)
    {

        horizontalDirection.Normalize();
        verticalDirection.Normalize();

        // Calculate the scalars a (horizontal) and b (vertical)
        float a = Vector3.Dot(worldPos - gridStartingCorner, horizontalDirection) / gridWorldSize.x;
        float b = Vector3.Dot(worldPos - gridStartingCorner, verticalDirection) / gridWorldSize.y;
        float percentX = Mathf.Clamp01(a);
        float percentY = Mathf.Clamp01(b);

        int x = Mathf.FloorToInt(Mathf.Clamp(GridRows * percentX, 0, GridRows - 1));
        int y = Mathf.FloorToInt(Mathf.Clamp(GridColumns * percentY, 0, GridColumns - 1));

        return grid[x, y];



        // float percentX = Math.Abs(worldPos.x - gridStartingCorner.x) / gridWorldSize.x;
        // float percentY = Math.Abs(worldPos.z - gridStartingCorner.z) / gridWorldSize.y;
        // percentX = Mathf.Clamp01(percentX);
        // percentY = Mathf.Clamp01(percentY);

        // int x = Mathf.FloorToInt(Mathf.Clamp(GridRows * percentX, 0, GridRows - 1));
        // int y = Mathf.FloorToInt(Mathf.Clamp(GridColumns * percentY, 0, GridColumns - 1));

        // return grid[x, y];
    }

    void SetPlaneVariables(GameObject plane)
    {
        if (plane != null)
        {
            MeshFilter meshFilter = plane.GetComponent<MeshFilter>();
            Bounds bounds = meshFilter.mesh.bounds;


            Vector3[] corners = new Vector3[4];


            Vector3 bottomLeft = new Vector3(bounds.min.x, bounds.min.y, bounds.min.z);
            Vector3 bottomRight = new Vector3(bounds.max.x, bounds.min.y, bounds.min.z);
            Vector3 topLeft = new Vector3(bounds.min.x, bounds.max.y, bounds.min.z);
            Vector3 topRight = new Vector3(bounds.max.x, bounds.max.y, bounds.min.z);


            // Convert to world space using TransformPoint
            corners[0] = plane.transform.TransformPoint(bottomLeft);
            corners[1] = plane.transform.TransformPoint(bottomRight);
            corners[2] = plane.transform.TransformPoint(topLeft);
            corners[3] = plane.transform.TransformPoint(topRight);

            gridStartingCorner.x = corners[0].x;
            gridStartingCorner.y = corners[0].y;
            gridStartingCorner.z = corners[0].z;

            Debug.Log(gridStartingCorner);

            horizontalDirection = (corners[1] - corners[0]).normalized;
            verticalDirection = (corners[2] - corners[0]).normalized;

            GridRows = (int)Math.Floor((corners[1] - corners[0]).magnitude / widthJump);
            GridColumns = (int)Math.Floor((corners[2] - corners[0]).magnitude / heightJump);

            Debug.Log((GridRows, GridColumns));

        }
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

    // void OldSetPlaneVariables(GameObject plane)
    // {
    //     if (plane != null)
    //     {
    //         Renderer renderer = plane.GetComponent<Renderer>();
    //         Bounds bounds = renderer.bounds;
    //         //Bounds bounds = plane.GetComponent<MeshFilter>().mesh.bounds;
    //         Vector3 bottomLeftCorner = plane.transform.TransformPoint(bounds.min);
    //         Vector3 topRightCorner = plane.transform.TransformPoint(bounds.max);

    //         gridStartingCorner.x = Math.Min(bottomLeftCorner.x, topRightCorner.x);
    //         gridStartingCorner.y = bottomLeftCorner.y + 0.1f;
    //         gridStartingCorner.z = Math.Min(bottomLeftCorner.z, topRightCorner.z);

    //         GridRows = (int)Math.Floor(Math.Abs(topRightCorner.x - bottomLeftCorner.x) / widthJump);
    //         GridColumns = (int)Math.Floor(Math.Abs(topRightCorner.z - bottomLeftCorner.z) / heightJump);
    //     }
    // }

}
