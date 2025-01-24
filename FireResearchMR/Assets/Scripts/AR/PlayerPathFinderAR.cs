using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using Newtonsoft.Json;

public class PlayerPathFinderAR : MonoBehaviour
{

    Dictionary<(int, int), float[]> qTable;

    public int MAXPATHLENGTH;
    public LineRenderer lineRenderer;
    public GridManagerAR grid;
    public Node fireNode;

    // Start is called before the first frame update
    void Start()
    {
        qTable = LoadDictionary();
        Debug.Log(qTable);
    }

    public void FindPath(Node playerNode)
    {
        int pathLength = 0;
        List<Node> path = new List<Node>();

        while (playerNode != fireNode && pathLength < MAXPATHLENGTH)
        {
            (int, int) obs = playerNode - fireNode;
            int choice = ArgMax(qTable[obs]);

            if (choice == 0) //up
            {
                playerNode = grid.GetNodeFromCoords(playerNode, 0, 1);
            }
            else if (choice == 1) //down
            {
                playerNode = grid.GetNodeFromCoords(playerNode, 0, -1);
            }
            else if (choice == 2) //left
            {
                playerNode = grid.GetNodeFromCoords(playerNode, -1, 0);
            }
            else if (choice == 3) //right
            {
                playerNode = grid.GetNodeFromCoords(playerNode, 1, 0);
            }

            path.Add(playerNode);

            pathLength++;
        }

        path.Add(fireNode);

        DrawPath(path);
    }

    void DrawPath(List<Node> path)
    {
        Vector3[] positions = new Vector3[path.Count];
        for (int i = 0; i < path.Count; i++)
        {
            positions[i] = path[i].worldPosition;
        }
        lineRenderer.positionCount = path.Count;
        lineRenderer.SetPositions(positions);
    }

    int ArgMax(float[] array)
    {
        if (array == null || array.Length == 0)
        {
            Debug.Log("Array is null or empty.");
            return -1; // Return an invalid index
        }

        int index = 0;
        float maxValue = array[0];

        for (int i = 1; i < array.Length; i++)
        {
            if (array[i] > maxValue)
            {
                maxValue = array[i];
                index = i;
            }
        }

        return index;
    }

    Dictionary<(int, int), float[]> LoadDictionary()
    {
        string filePath = Path.Combine(Application.persistentDataPath, "dictionary.json");

        if (!File.Exists(filePath))
        {
            Debug.Log("Dictionary not found");
            return null;
        }

        string json = File.ReadAllText(filePath);
        var serializableDict = JsonConvert.DeserializeObject<Dictionary<string, float[]>>(json);

        // Convert back to Dictionary<(int, int), TValue>
        var loadedDict = new Dictionary<(int, int), float[]>();
        foreach (var kvp in serializableDict)
        {
            var key = ParseTupleKey(kvp.Key);
            loadedDict.Add(key, kvp.Value);
        }

        return loadedDict;
    }

    private (int, int) ParseTupleKey(string key)
    {
        // Parse the string "(x, y)" into a ValueTuple<int, int>
        key = key.Trim('(', ')');
        var parts = key.Split(',');
        return (int.Parse(parts[0]), int.Parse(parts[1]));
    }
}
