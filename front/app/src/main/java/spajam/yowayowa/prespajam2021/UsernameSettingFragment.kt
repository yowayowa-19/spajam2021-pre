package spajam.yowayowa.prespajam2021

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import com.fingerprintjs.android.fingerprint.Configuration
import com.fingerprintjs.android.fingerprint.FingerprinterFactory
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import org.json.JSONObject
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody


class UsernameSettingFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_username_setting, container, false)
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val button = view.findViewById<Button>(R.id.button)
        val editText = view.findViewById<EditText>(R.id.editTextTextPersonName)
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
                button.isEnabled = !(s.length === 0)
            }
        })
        button.setOnClickListener(){
            val fingerprinter = FingerprinterFactory
                .getInstance(requireContext(), Configuration(version = 3))

            fingerprinter.getDeviceId { result ->
                val deviceId = result.deviceId
                postToServer(deviceId,editText.text.toString())
            }
            val manager: FragmentManager? = activity?.supportFragmentManager
            val transaction: FragmentTransaction? = manager?.beginTransaction()
            transaction?.add(R.id.frameLayout, PairingSettingFragment())
            transaction?.commit()
        }
    }
    private fun postToServer(deviceId : String, userName: String){
        GlobalScope.launch {
            try {
                val url: String = "http://192.168.30.134:8000/mobile/register/"
                val client: OkHttpClient = OkHttpClient.Builder().build()

                // create json
                val json = JSONObject()
                json.put("mac_address", deviceId)
                json.put("user_name", userName)

                // post
                val postBody =
                    json.toString().toRequestBody("application/json; charset=utf-8".toMediaTypeOrNull())
                val request: Request = Request.Builder().url(url).post(postBody).build()
                val response = client.newCall(request).execute()

                val result: String = response.body!!.string()
                Log.d("tag",result)
                response.close()
            }catch (e : Exception){
                Log.d("err",e.toString())
            }
        }
    }
}