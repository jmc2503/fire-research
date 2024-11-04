using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour
{

    public int GridRows;
    public int GridColumns;
    public float BoxSeparation;
    public Vector2 gridStartingCorner;

    public GameObject gridBox;

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

        grid = new Node[GridRows, GridColumns];

        CreateGrid();
    }

    void CreateGrid()
    {
        for (int i = 0; i < GridRows; i++)
        {
            for (int j = 0; j < GridColumns; j++)
            {
                Vector3 worldPos = new Vector3(gridStartingCorner.x + i * widthJump, 0, gridStartingCorner.y + j * heightJump);
                grid[i, j] = new Node(worldPos, Instantiate(gridBox, worldPos, Quaternion.identity));
            }
        }
    }

    public Node GetNodeFromWorldPoint(Vector3 worldPos)
    {
        float percentX = (worldPos.x + gridWorldSize.x / 2) / gridWorldSize.x;
        float percentY = (worldPos.z + gridWorldSize.y / 2) / gridWorldSize.y;
        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.FloorToInt(Mathf.Clamp(GridRows * percentX, 0, GridRows - 1));
        int y = Mathf.FloorToInt(Mathf.Clamp(GridColumns * percentY, 0, GridColumns - 1));

        return grid[x, y];
    }
}
