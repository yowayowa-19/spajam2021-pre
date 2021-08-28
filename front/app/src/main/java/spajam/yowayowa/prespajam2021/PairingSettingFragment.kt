package spajam.yowayowa.prespajam2021

import android.os.Bundle
import android.text.Editable
import android.text.InputFilter
import android.text.InputFilter.LengthFilter
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
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
        val button = view.findViewById<Button>(R.id.button)
        button.setOnClickListener(){
            val manager: FragmentManager? = activity?.supportFragmentManager
            val transaction: FragmentTransaction? = manager?.beginTransaction()
            transaction?.add(R.id.frameLayout, UsernameSettingFragment())
            transaction?.commit()
        }
        val editText = view.findViewById<EditText>(R.id.editTextPairingStr)
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
}