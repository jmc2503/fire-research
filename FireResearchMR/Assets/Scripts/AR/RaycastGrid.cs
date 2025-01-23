using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using EnhancedTouch = UnityEngine.InputSystem.EnhancedTouch;

public class RayCastGrid : MonoBehaviour
{

    public GridManager gridManager;

    private bool gridCreated;
    ARRaycastManager arRayMan;
    List<ARRaycastHit> hits = new List<ARRaycastHit>();

    void Start()
    {
        arRayMan = GetComponent<ARRaycastManager>();
        gridCreated = false;
    }

    private void OnEnable()
    {
        EnhancedTouch.TouchSimulation.Enable();
        EnhancedTouch.EnhancedTouchSupport.Enable();
        EnhancedTouch.Touch.onFingerDown += FingerDown;
    }

    private void OnDisable()
    {
        EnhancedTouch.TouchSimulation.Disable();
        EnhancedTouch.EnhancedTouchSupport.Disable();
        EnhancedTouch.Touch.onFingerDown -= FingerDown;
    }

    private void FingerDown(EnhancedTouch.Finger finger)
    {
        if (finger.index != 0)
        {
            return;
        }

        PlaceGrid(finger.currentTouch.screenPosition);
    }

    private void PlaceGrid(Vector2 screenPosition)
    {
        if (arRayMan.Raycast(screenPosition, hits, TrackableType.PlaneWithinPolygon))
        {

            var hitpose = hits[0].pose;

            if (!gridCreated)
            {
                gridManager.gameObject.transform.position = hitpose.position;
                gridManager.gridStartingCorner = hitpose.position;
                gridCreated = true;
            }
        }
    }
}
