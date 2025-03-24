using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Meta.XR.MRUtilityKit;
using TMPro;
using System.IO;

public class PlayerControllerEscape : MonoBehaviour
{
    public int maxHealth;
    public HealthBar healthBar;
    public TextMeshProUGUI healthText;

    public GameObject menu;
    public Transform head;
    public float spawnDistance = 2f;

    private int currentHealth;

    //Tracking framerate
    private List<float> frameRates = new List<float>();
    private string filePath;

    // Start is called before the first frame update
    void Start()
    {
        currentHealth = maxHealth;
        healthBar.SetMaxHealth(maxHealth);
        healthText.text = "Health: " + currentHealth.ToString();

        filePath = Path.Combine(Application.persistentDataPath, "FrameRateData.txt");


    }

    void Update()
    {
        frameRates.Add(1.0f / Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.C) || OVRInput.GetDown(OVRInput.Button.Start))
        {
            menu.SetActive(!menu.activeSelf);

            menu.transform.position = head.position + new Vector3(head.forward.x, 0, head.forward.z).normalized * spawnDistance;
        }
        else if (Input.GetKeyDown(KeyCode.Space) || OVRInput.GetDown(OVRInput.Button.PrimaryHandTrigger))
        {
            SaveToFile();
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

    void SaveToFile()
    {
        using (StreamWriter writer = new StreamWriter(filePath, false))
        {
            foreach (float fps in frameRates)
            {
                writer.WriteLine(fps);
            }
        }
        Debug.Log("Frame rate log saved to: " + filePath);
    }
}

