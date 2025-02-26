using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerControllerEscape : MonoBehaviour
{
    public int maxHealth;

    private int currentHealth;

    public HealthBar healthBar;

    // Start is called before the first frame update
    void Start()
    {
        currentHealth = maxHealth;
        healthBar.SetMaxHealth(maxHealth);
    }

    public void DamagePlayer(int damage)
    {
        currentHealth -= damage;
        healthBar.SetHealth(currentHealth);
        if (currentHealth <= 0)
        {
            Debug.Log("Dead");
        }
    }
}
