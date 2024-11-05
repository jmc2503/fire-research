using System.Collections;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;
using Unity.VisualScripting;
using UnityEngine;

public class GridManager : MonoBehaviour
{

    public int GridRows;
    public int GridColumns;
    public float BoxSeparation;
    public Vector2 gridStartingCorner;

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

        if (x - 1 >= 0 && !grid[x - 1, y].OnFire)
        {
            availableNodes.Add(grid[x - 1, y]);
        }
        if (x + 1 < GridRows && !grid[x - 1, y].OnFire)
        {
            availableNodes.Add(grid[x - 1, y]);
        }
        if (y - 1 >= 0 && !grid[x, y - 1].OnFire)
        {
            availableNodes.Add(grid[x, y - 1]);
        }
        if (y + 1 < GridColumns && !grid[x, y + 1].OnFire)
        {
            availableNodes.Add(grid[x, y + 1]);
        }
        return availableNodes;
    }
}
