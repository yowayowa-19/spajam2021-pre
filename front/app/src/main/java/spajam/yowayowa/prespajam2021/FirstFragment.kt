package spajam.yowayowa.prespajam2021

import android.content.Context.SENSOR_SERVICE
import android.hardware.*
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.core.content.ContextCompat.getSystemService
import androidx.navigation.fragment.findNavController
import okhttp3.*
import java.io.IOException
import android.util.Log

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FirstFragment : Fragment(){

    private var mSensorManager: SensorManager? = null
    private var mAccelerometer: Sensor? = null
    private var mShakeDetector: ShakeDetector? = null

    override fun onCreateView(
            inflater: LayoutInflater, container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        initSensor()
        return inflater.inflate(R.layout.fragment_first, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        mSensorManager!!.registerListener(
            mShakeDetector,
            mAccelerometer,
            SensorManager.SENSOR_DELAY_UI
        )
    }

    override fun onStop() {
        super.onStop()
        mSensorManager?.unregisterListener(this.mShakeDetector);
    }

    private fun initSensor() {
        // ShakeDetector initialization
        mSensorManager = activity?.getSystemService(SENSOR_SERVICE) as SensorManager
        mAccelerometer = mSensorManager!!.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        mShakeDetector = ShakeDetector()
        mShakeDetector!!.setOnShakeListener(object : ShakeDetector.OnShakeListener {
            override fun onShake(count: Int) { /*
                 * The following method, "handleShakeEvent(count):" is a stub //
                 * method you would use to setup whatever you want done once the
                 * device has been shook.
                 */
                //Toast.makeText(activity, count.toString(), Toast.LENGTH_SHORT).show()
                getToServer()
            }
        })
    }

    internal fun getToServer() {
        val url: String = "http://192.168.30.134:8000"
        val client: OkHttpClient = OkHttpClient()
        val request = Request.Builder().url(url).get().build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.d("tag","Fail.")
                Log.d("tag",e.toString())
            }

            override fun onResponse(call: Call, response: Response) {
                val responseText: String? = response.body?.string()
                if(responseText === null) return
                Log.d("tag",responseText)
            }
        })
    }
}