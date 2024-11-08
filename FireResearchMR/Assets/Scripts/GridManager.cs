using System.Collections;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;
using Unity.VisualScripting;
using UnityEngine;

public class GridManager : MonoBehaviour
{
    [Header("SCRIPTS")]
    public FireManager fireManager;

    [Header("PARAMETERS")]
    public int GridRows;
    public int GridColumns;
    public float BoxSeparation;
    public Vector2 gridStartingCorner;
    public Vector2 fireStartPoint;

    [Header("GAMEOBJECTS")]
    public GameObject gridBox;
    public Material[] materials;

    private float nodeRadius;
    private Node[,] grid;
    private float widthJump;
    private float heightJump;
    private Vector2 gridWorldSize;

    // Start is called before the first frame update
    void Start()
    {
        Renderer renderer = gridBox.GetComponent<Renderer>();
        Vector3 gridBoxSize = renderer.bounds.size;

        //Establish constants
        widthJump = gridBoxSize.x + BoxSeparation;
        heightJump = gridBoxSize.z + BoxSeparation;
        gridWorldSize.x = widthJump * GridRows;
        gridWorldSize.y = heightJump * GridColumns;

        nodeRadius = widthJump / 2;

        grid = new Node[GridRows, GridColumns];

        CreateGrid();
        fireManager.StartFire(grid[(int)fireStartPoint.x, (int)fireStartPoint.y]);
    }

    void CreateGrid()
    {
        for (int i = 0; i < GridRows; i++)
        {
            for (int j = 0; j < GridColumns; j++)
            {
                Vector3 worldPos = new Vector3(gridStartingCorner.x + (i * widthJump + nodeRadius), 0, gridStartingCorner.y + (j * heightJump + nodeRadius));
                grid[i, j] = new Node(i, j, worldPos, Instantiate(gridBox, worldPos, Quaternion.identity), materials);
            }
        }
    }

    public Node GetNodeFromWorldPoint(Vector3 worldPos)
    {
        //float percentX = (worldPos.x + gridWorldSize.x / 2) / gridWorldSize.x;
        //float percentY = (worldPos.z + gridWorldSize.y / 2) / gridWorldSize.y;
        float percentX = worldPos.x / gridWorldSize.x;
        float percentY = worldPos.z / gridWorldSize.y;
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

    public Vector3[,] GetIndicatorPositions(Node currNode, int viewDistance)
    {
        Vector3[,] positions = new Vector3[4, viewDistance];

        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < viewDistance; j++)
            {
                Vector3 newPos = currNode.worldPosition;
                int adjustedJ = j + 1;
                if (i == 0)
                { //Left indicators
                    newPos.x += adjustedJ * (-widthJump);
                }
                else if (i == 1) //right indicators
                {
                    newPos.x += adjustedJ * (widthJump);
                }
                else if (i == 2) //down indicators
                {
                    newPos.z += adjustedJ * (-heightJump);
                }
                else
                {
                    newPos.z += adjustedJ * (heightJump);
                }
                positions[i, j] = newPos;
            }
        }

        return positions;
    }
}
