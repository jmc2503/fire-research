using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QLearningAgent : MonoBehaviour
{

    [Header("PARAMETERS")]
    public float LEARNING_RATE;
    public float DISCOUNT;
    public float EPSILON;
    public float EPS_DECAY;
    public float NUM_EPISODES;
    public float EPISODE_LENGTH;

    [Header("REWARDS")]
    public int FIRE_REWARD;
    public int MOVE_PENALTY;

    [Header("Scripts")]
    public GridManager GridManager;

    private Dictionary<((int, int), (int, int)), float[]> qTable;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void CreateQTable(){
        
        int rows = GridManager.GridRows;
        int cols = GridManager.GridColumns;
        
        for(int x1 = -rows; x1 < rows; x1++){
            for(int y1 = -cols; y1 < cols; y1++){
                for(int x2 = -rows; x2 < rows; x2++){
                    for(int y2 = -cols; y2 < cols; y2++){
                        qTable[((x1,y1),(x2,y2))] = null;
                    }
                }
            }
        }
    }
}
