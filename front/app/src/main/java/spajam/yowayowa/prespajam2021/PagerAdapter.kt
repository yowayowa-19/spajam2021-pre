package spajam.yowayowa.prespajam2021

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.fragment.app.FragmentManager
import androidx.viewpager2.adapter.FragmentStateAdapter

class PagerAdapter(fm: FragmentActivity): FragmentStateAdapter(fm)  {
    private val res : List<Fragment> = listOf<Fragment>(
        FirstFragment(),
        SecondFragment()
    )

    override fun createFragment(position: Int): Fragment {
        return res[position]
    }

    override fun getItemCount(): Int {
        return res.size
    }

}