using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class QLearningAgent : MonoBehaviour
{

    [Header("PARAMETERS")]
    public float LEARNING_RATE;
    public float DISCOUNT;
    public float EPSILON;
    public float EPS_DECAY;
    public int NUM_EPISODES;
    public int EPISODE_LENGTH;

    [Header("REWARDS")]
    public int FIRE_REWARD;
    public int MOVE_PENALTY;
    public float[] episode_reward_list;

    [Header("Scripts")]
    public GridManager GridManager;

    [Header("Positions")]
    public Vector2 fireStartPos;
    public Vector2 playerStartPos;

    private Dictionary<(int, int), float[]> qTable;
    private Node[,] grid;
    private Node playerNode;
    private Node fireNode;
    private int rows;
    private int cols;

    // Start is called before the first frame update
    void Start()
    {
        CreateQTable();
        rows = GridManager.GridRows;
        cols = GridManager.GridColumns;
        grid = new Node[rows, cols];
        GridManager.CreateGrid(grid);
        episode_reward_list = new float[NUM_EPISODES];
    }

    // Update is called once per frame
    void Update()
    {

    }

    void CreateQTable()
    {

        for (int x1 = -rows; x1 < rows; x1++)
        {
            for (int y1 = -cols; y1 < cols; y1++)
            {

                qTable[(x1, y1)] = new float[4];
            }
        }
    }

    void Train()
    {
        for (int episode = 0; episode < NUM_EPISODES; episode++)
        {

            float episode_reward = 0;

            for (int step = 0; step < EPISODE_LENGTH; step++)
            {
                (int, int) obs = playerNode - fireNode;

                int a = 0;

                if (Random.value > EPSILON)
                {
                    a = ArgMax(qTable[obs]);
                }
                else
                {
                    a = Random.Range(0, 4);
                }

                action(a);

                float reward = 0;

                if (playerNode == fireNode)
                {
                    reward += FIRE_REWARD;
                }
                else
                {
                    reward += MOVE_PENALTY;
                }

                (int, int) new_obs = playerNode - fireNode;
                float max_future_q = Max(qTable[new_obs]);
                float current_q = qTable[new_obs][a];

                float new_q = 0;

                if (reward == FIRE_REWARD)
                {
                    new_q = reward;
                }
                else
                {
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q);
                }

                qTable[obs][a] = new_q;

                episode_reward += reward;

                if (reward == FIRE_REWARD)
                {
                    break;
                }

            }

            episode_reward_list[episode] = episode_reward;

            EPSILON *= EPS_DECAY;
        }
    }

    void action(int choice)
    {
        if (choice == 0)
        { //up
            move(0, 1);
        }
        else if (choice == 1)
        { //down
            move(0, -1);
        }
        else if (choice == 2)
        { //left
            move(-1, 0);
        }
        else if (choice == 3)
        { //right
            move(1, 0);
        }
    }

    void move(int x, int y)
    {
        int new_x = playerNode.x + x;
        int new_y = playerNode.y + y;

        if (new_x < 0)
        {
            new_x = 0;
        }
        else if (new_x >= rows)
        {
            new_x = rows - 1;
        }

        if (new_y < 0)
        {
            new_y = 0;
        }
        else if (new_y >= cols)
        {
            new_y = cols - 1;
        }

        playerNode.HasPlayer = false;
        playerNode = grid[new_x, new_y];
        playerNode.HasPlayer = true;
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

    float Max(float[] array)
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

        return maxValue;
    }

}
