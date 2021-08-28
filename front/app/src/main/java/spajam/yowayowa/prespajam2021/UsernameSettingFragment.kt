package spajam.yowayowa.prespajam2021

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import androidx.fragment.app.Fragment
import org.w3c.dom.Text


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
        button.setOnClickListener(){
            val intent = Intent(activity, MainActivity::class.java)
            //戻ってこれなくする
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK
            startActivity(intent)
        }
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
    }
}