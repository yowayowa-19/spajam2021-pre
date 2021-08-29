package spajam.yowayowa.prespajam2021

import android.content.Context.SENSOR_SERVICE
import android.content.Intent
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
import android.widget.ImageView
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import com.fingerprintjs.android.fingerprint.Configuration
import com.fingerprintjs.android.fingerprint.FingerprinterFactory
import kotlinx.coroutines.runBlocking
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class ThirdFragment : Fragment(){

    private var mSensorManager: SensorManager? = null
    private var mAccelerometer: Sensor? = null
    private var mShakeDetector: ShakeDetector? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        initSensor()
        return inflater.inflate(R.layout.fragment_third, container, false)
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
                val fingerprinter = FingerprinterFactory
                    .getInstance(requireContext(), Configuration(version = 3))

                fingerprinter.getDeviceId { result ->
                    val deviceId = result.deviceId
                    val tf = postToServer(deviceId)
                    if (tf){
                        activity?.runOnUiThread {
                            Toast.makeText(
                                context,
                                "認証に成功しました。",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                        val manager: FragmentManager? = activity?.supportFragmentManager
                        val transaction: FragmentTransaction? = manager?.beginTransaction()
                        transaction?.add(R.id.nav_host_fragment, ForthFragment())
                        transaction?.commit()
                    }else{
                        activity?.runOnUiThread {
                            Toast.makeText(
                                context,
                                "認証に失敗しました。\nもう一度やりなおしてください。",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }
                }
            }
        })
    }

    internal fun postToServer(deviceId : String) : Boolean {
        return runBlocking {
            try {
                val url: String = "http://192.168.30.134:8000/mobile/stop"

                val client: OkHttpClient = OkHttpClient()
                // create json
                val json = JSONObject()
                json.put("mac_address", deviceId)
                // post
                val postBody =
                    json.toString().toRequestBody("application/json; charset=utf-8".toMediaTypeOrNull())
                val request: Request = Request.Builder().url(url).post(postBody).build()
                val response = client.newCall(request).execute()

                val result: String = response.body!!.string()
                Log.d("tag",result)
                response.close()
                return@runBlocking result.contains("true")
            }catch (e : Exception){
                Log.d("err",e.toString())
                return@runBlocking false
            }
        }
    }
}