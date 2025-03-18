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

    public GameObject menu;
    public Transform head;
    public float spawnDistance = 2f;

    private int currentHealth;

    // Start is called before the first frame update
    void Start()
    {
        currentHealth = maxHealth;
        healthBar.SetMaxHealth(maxHealth);
        healthText.text = "Health: " + currentHealth.ToString();
    }

    void Update()
    {

        if (Input.GetKeyDown(KeyCode.C) || OVRInput.GetDown(OVRInput.Button.Start))
        {
            menu.SetActive(!menu.activeSelf);

            menu.transform.position = head.position + new Vector3(head.forward.x, 0, head.forward.z).normalized * spawnDistance;
        }
        menu.transform.LookAt(new Vector3(head.position.x, menu.transform.position.y, head.position.z));
        menu.transform.forward *= -1;
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
