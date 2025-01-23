using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.InputSystem;

public class QLearningAgent : MonoBehaviour
{

    [Header("PARAMETERS")] //Various Q Learning Hyperparameters
    public float LEARNING_RATE;
    public float DISCOUNT;
    public float EPSILON;
    public float EPS_DECAY;
    public int NUM_EPISODES;
    public int EPISODE_LENGTH;

    [Header("REWARDS")] //Rewards and Reward Tracking
    public int FIRE_REWARD;
    public int MOVE_PENALTY;
    private float[] episode_reward_list;

    [Header("Scripts")] //Script Links
    public GridManager GridManager;

    private Dictionary<(int, int), float[]> qTable; //qTable takes distance to fire as input and holds 4 float list of possible actions
    private Node[,] grid;

    //These track the player and fire location
    private Node playerNode;
    private Node fireNode;

    //Size of grid
    private int rows;
    private int cols;

    private bool trainingComplete = false;

    // Start is called before the first frame update
    void Start()
    {
        //Initialization of variables
        rows = GridManager.GridRows;
        cols = GridManager.GridColumns;
        grid = new Node[rows, cols];
        GridManager.CreateGrid(grid);

        episode_reward_list = new float[NUM_EPISODES];

        CreateQTable();
    }

    // Update is called once per frame
    void Update()
    {
        //Only allow training to occur once using trainingComplete flag variable
        if (!trainingComplete && Input.GetKeyDown(KeyCode.Space))
        {
            Train();
            trainingComplete = true;
        }
    }

    void CreateQTable()
    {
        //Create qTable of all possible distances that fire can be from player using size of grid
        qTable = new Dictionary<(int, int), float[]>();

        for (int x1 = -rows; x1 < rows; x1++)
        {
            for (int y1 = -cols; y1 < cols; y1++)
            {
                qTable[(x1, y1)] = new float[4]; //list of size 4 to represent going up, down, left, right
            }
        }
    }

    async void Train()
    {
        //Loop through episodes
        for (int episode = 0; episode < NUM_EPISODES; episode++)
        {

            float episode_reward = 0;

            //Generate starting locations for player and fire randomly
            (int, int) playerStart = GenerateRandomStart();
            (int, int) fireStart = GenerateRandomStart();

            //Set the nodes by getting them from the grid
            playerNode = grid[playerStart.Item1, playerStart.Item2];
            playerNode.HasPlayer = true;

            fireNode = grid[fireStart.Item1, fireStart.Item2];
            fireNode.OnFire = true;
            fireNode.Hidden = false;

            //Loop through steps of an episode
            for (int step = 0; step < EPISODE_LENGTH; step++)
            {
                (int, int) obs = playerNode - fireNode; //subtraction operator overwritten in Node class

                int a = 0;

                //Generate random action or best action using epsilon greedy policy
                if (Random.value > EPSILON)
                {
                    a = ArgMax(qTable[obs]);
                }
                else
                {
                    a = Random.Range(0, 4);
                }

                action(a);

                await Task.Delay(10); //delay purely for visuals in unity editor

                float reward = 0;

                //Check for rewards
                if (playerNode == fireNode)
                {
                    reward += FIRE_REWARD;
                }
                else
                {
                    reward -= MOVE_PENALTY;
                }

                //Update qTable using basic Q Learning rule
                (int, int) new_obs = playerNode - fireNode;
                float max_future_q = Max(qTable[new_obs]);
                float current_q = qTable[new_obs][a];

                float new_q = 0;

                if (reward == FIRE_REWARD)
                {
                    new_q = reward; //found fire this state should just be maximized
                }
                else
                {
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q);
                }

                qTable[obs][a] = new_q;

                episode_reward += reward;

                //Stop iterating if the fire was found
                if (reward == FIRE_REWARD)
                {
                    break;
                }

            }

            //Clean up, track results, and decay epsilon
            episode_reward_list[episode] = episode_reward;
            playerNode.HasPlayer = false;
            fireNode.OnFire = false;
            fireNode.Hidden = true;
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

        //Boundary checking for valid moves
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

    (int, int) GenerateRandomStart()
    {
        int x = Random.Range(0, rows);
        int y = Random.Range(0, cols);

        return (x, y);
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
