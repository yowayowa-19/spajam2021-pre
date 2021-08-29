package spajam.yowayowa.prespajam2021

import android.R.attr.data
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.ListView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import okhttp3.*


/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class SecondFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_second, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        /*
        val listView = view.findViewById<ListView>(R.id.listView)
        val arrayList = ArrayList<String>()
        arrayList.add("ria")
        arrayList.add("riaa")
        arrayList.add("riaaa")
        arrayList.add("riaaaa")
        val mAdapter: ArrayAdapter<*> = ArrayAdapter<String>(requireContext(), android.R.layout.simple_list_item_1, arrayList)
        listView.adapter = mAdapter
        view.findViewById<Button>(R.id.button_second).setOnClickListener {
            val intent = Intent(context, WalkThroughActivity::class.java)
            //帰ってこれなくする
            startActivity(intent)
        }
        */
    }
}
