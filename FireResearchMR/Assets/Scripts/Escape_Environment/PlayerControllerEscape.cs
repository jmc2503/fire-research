using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Meta.XR.MRUtilityKit;
using TMPro;

public class PlayerControllerEscape : MonoBehaviour
{
    public int maxHealth;
    public HealthBar healthBar;
    public TextMeshProUGUI healthText;

    public GridManagerEscape grid;
    public EffectMesh effectmesh;

    private int currentHealth;
    private bool flag = false; //flag to toggle effect meshes

    // Start is called before the first frame update
    void Start()
    {
        currentHealth = maxHealth;
        healthBar.SetMaxHealth(maxHealth);
        healthText.text = "Health: " + currentHealth.ToString();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.A) || OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger))
        {
            grid.HideGridBoxes();
        }

        if (Input.GetKeyDown(KeyCode.B) || OVRInput.GetDown(OVRInput.Button.SecondaryIndexTrigger))
        {
            if (effectmesh != null)
            {
                if (flag)
                {
                    effectmesh.HideMesh = true;
                    flag = !flag;
                }
                else
                {
                    effectmesh.HideMesh = false;
                    flag = !flag;
                }
            }
        }
    }

    public void DamagePlayer(int damage)
    {
        currentHealth -= damage;
        healthBar.SetHealth(currentHealth);
        healthText.text = "Health: " + currentHealth.ToString();

        if (currentHealth <= 0)
        {
            healthText.text = "Dead";
        }
    }
}
