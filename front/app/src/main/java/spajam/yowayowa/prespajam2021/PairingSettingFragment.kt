package spajam.yowayowa.prespajam2021

import android.os.Bundle
import android.text.Editable
import android.text.InputFilter
import android.text.InputFilter.LengthFilter
import android.text.TextWatcher
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import com.fingerprintjs.android.fingerprint.Configuration
import com.fingerprintjs.android.fingerprint.FingerprinterFactory
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.*


class PairingSettingFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_pairing_setting, container, false)
    }

    // アルファベットフィルタ
    private val alphabetFilter =
        InputFilter { source, start, end, dest, dstart, dend ->
            if (source.toString().matches(Regex("^[a-zA-Z]{0,8}+$"))) {
                source.toString().toUpperCase(Locale.ROOT)
            } else {
                ""
            }
        }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val editText = view.findViewById<EditText>(R.id.editTextPairingStr)
        val button = view.findViewById<Button>(R.id.button)
        button.setOnClickListener(){
            val fingerprinter = FingerprinterFactory
                .getInstance(requireContext(), Configuration(version = 3))

            fingerprinter.getDeviceId { result ->
                val deviceId = result.deviceId
                val tf = postToServer(deviceId,editText.text.toString())
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
                    transaction?.add(R.id.frameLayout, UsernameSettingFragment())
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
        val myFilters = arrayOf(alphabetFilter, LengthFilter(5))
        editText.filters = myFilters
        editText.addTextChangedListener(object : TextWatcher {
            // 文字列sのなかで startの位置から開始されている字数countの文字が、
            // 字数lengthの古いテキストを置換するときに呼び出される。
            override fun onTextChanged(s: CharSequence, start: Int, before: Int, count: Int) {
                // TODO Auto-generated method stub
            }

            // 文字列sのなかで startの位置から開始されている字数countの文字が、
            // 字数lengthの新しいテキストで置換されようとしているときに呼び出される。
            override fun beforeTextChanged(s: CharSequence, start: Int, count: Int, after: Int) {
                // TODO Auto-generated method stub
            }

            // 文字列sのどこかで、テキストが変更されたときに呼び出される。
            override fun afterTextChanged(s: Editable) {
                button.isEnabled = (s.length === 5)
            }
        })
    }

    private fun postToServer(deviceId : String, phrase: String) : Boolean{
        return runBlocking {
            try {
                val url: String = "http://192.168.30.134:8000/mobile/pairing/"
                val client: OkHttpClient = OkHttpClient.Builder().build()

                // create json
                val json = JSONObject()
                json.put("mac_address", deviceId)
                json.put("phrase", phrase)

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